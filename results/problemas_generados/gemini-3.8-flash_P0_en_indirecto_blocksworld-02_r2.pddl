(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (handempty)
    (on c b)
    (ontable b)
    (clear c)
    (ontable a)
    (clear a)
    (ontable d)
    (clear d)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
