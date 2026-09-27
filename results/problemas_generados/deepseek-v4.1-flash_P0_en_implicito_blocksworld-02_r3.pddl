(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (clear a)
    (ontable d)
    (clear d)
    (ontable b)
    (on c b)
    (clear c)
    (handempty)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
