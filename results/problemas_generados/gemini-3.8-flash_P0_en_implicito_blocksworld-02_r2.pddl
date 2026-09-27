(define (problem blocks-4-0)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (handempty)
    (ontable a)
    (clear a)
    (ontable d)
    (clear d)
    (ontable b)
    (on c b)
    (clear c)
  )
  (:goal
    (and
      (on a b)
      (on b c)
      (on c d)
    )
  )
)
