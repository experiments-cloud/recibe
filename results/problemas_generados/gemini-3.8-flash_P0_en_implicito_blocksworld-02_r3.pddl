(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (clear a)
    (clear c)
    (clear d)
    (ontable a)
    (ontable b)
    (ontable d)
    (on c b)
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
