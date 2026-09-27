(define (problem blocks-7-0)
  (:domain BLOCKS)
  (:objects
    a b c d e f g - block
  )
  (:init
    (handempty)
    (ontable d)
    (ontable f)
    (on a d)
    (on b c)
    (on c g)
    (on g e)
    (on e f)
    (clear a)
    (clear b)
  )
  (:goal
    (and
      (on a c)
      (on b f)
      (on c g)
      (on d a)
      (on e b)
      (on f d)
    )
  )
)
